"""
AI Chat Agent for Todo Management
Uses Cohere to process natural language and interact with tasks via MCP tools
"""

import os
import logging
from typing import Dict, Any, List
from pydantic import BaseModel
import cohere

from .config import agent_config
from mcp.tools.task_operations import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)
from mcp.tools.task_operations import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
from .task_resolver import resolve_task_by_reference, find_potential_task_matches, needs_clarification

# Set up logging
logger = logging.getLogger(__name__)


async def run_chat_agent(
    user_id: str,
    user_message: str,
    conversation_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Run the chat agent to process user input and generate responses
    """
    logger.info(f"Processing chat request for user {user_id}: {user_message[:50]}...")

    # Initialize Cohere client
    co = agent_config.get_cohere_client()

    # Prepare the conversation context for the model
    # Create a system prompt based on the Phase III constitution
    system_prompt = f"""
    You are a helpful AI assistant for managing todo tasks. You have access to the following tools:

    - add_task: Add a new task for the user
    - list_tasks: List tasks for the user with optional status filter
    - complete_task: Mark a task as completed
    - delete_task: Delete a task
    - update_task: Update a task's title, description, or priority

    When the user wants to:
    - Add a task: Use add_task with user_id and title (and optional description)
    - See tasks: Use list_tasks with user_id and optional status ("all", "pending", "completed")
    - Complete a task: Use complete_task with user_id and task_id
    - Delete a task: Use delete_task with user_id and task_id
    - Update a task: Use update_task with user_id, task_id, and optional title/description/priority

    Always use the appropriate tool to interact with tasks rather than making up information.
    When listing tasks, clearly show the task IDs so the user can reference them later.
    If a user asks about their email/login, respond based on the user_id context provided (user_id: {user_id}).
    Always be helpful and confirm actions taken.

    TASK REFERENCE GUIDELINES:
    - Users may refer to tasks by name/title instead of ID (e.g., "complete the grocery task")
    - When a user refers to a task by name, use the task_id parameter with the name/text
    - The system will automatically resolve the name to the correct task ID
    - If a task name could match multiple tasks, the system will ask for clarification
    - You can also use numeric task IDs when known (e.g., task_id: "123")

    DISAMBIGUATION RULES:
    - If a user refers to a task by name/title that could match multiple tasks, the system will automatically ask for clarification
    - If a user says "complete the meeting task" but there are multiple tasks containing "meeting", the system will show options for clarification
    - When in doubt, list the relevant tasks first and ask the user to specify which one they mean
    - Always confirm the specific task ID before performing operations like delete, complete, or update

    IMPORTANT: When the user sends a message, determine if you need to call any tools.
    If you need to call a tool, respond with JSON in the format:
    {{
        "tool_calls": [
            {{
                "name": "tool_name",
                "arguments": {{
                    "user_id": "{user_id}",
                    "task_id": "task identifier (name or ID)"
                }}
            }}
        ],
        "response": "optional message to user while tools execute"
    }}

    If you don't need to call any tools, respond with:
    {{
        "response": "your response to the user"
    }}
    """

    # Prepare chat history for Cohere API
    # The Cohere API expects chat_history to be a list of dictionaries with "role" and "message" keys
    # Roles must be in the format: "User", "Chatbot", "System", "Tool"
    formatted_chat_history = []
    if len(conversation_history) > 1:
        for hist_msg in conversation_history[:-1]:  # Exclude the current message
            # Convert database role format to Cohere-compatible format
            db_role = hist_msg["role"]
            if db_role.lower() == "user":
                cohere_role = "User"
            elif db_role.lower() == "assistant":
                cohere_role = "Chatbot"
            elif db_role.lower() == "system":
                cohere_role = "System"
            else:
                # Default to "User" if unknown role, though this shouldn't happen
                cohere_role = "User"

            # Ensure each history message has the correct format for Cohere API
            formatted_message = {
                "role": cohere_role,
                "message": hist_msg["content"]  # Cohere expects "message" instead of "content"
            }
            formatted_chat_history.append(formatted_message)

    try:
        # Call Cohere's chat endpoint
        logger.debug(f"Calling Cohere API for user {user_id}")
        response = co.chat(
            message=user_message,
            preamble=system_prompt,
            chat_history=formatted_chat_history,
            model=agent_config.COHERE_MODEL,
            temperature=agent_config.TEMPERATURE,
        )
        logger.debug(f"Cohere API call successful for user {user_id}")

        # Process the response
        response_text = response.text

        # Parse the response to see if it contains tool calls
        import json
        import re

        # Look for JSON in the response that indicates tool calls
        tool_calls = []
        tool_results = []

        # Check if response contains JSON with tool calls
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                parsed_json = json.loads(json_match.group())

                if "tool_calls" in parsed_json:
                    logger.info(f"Processing {len(parsed_json['tool_calls'])} tool calls for user {user_id}")

                    # Process tool calls
                    for tool_call in parsed_json["tool_calls"]:
                        tool_name = tool_call["name"]
                        arguments = tool_call["arguments"]

                        # Add user_id to arguments if not already present
                        if 'user_id' not in arguments:
                            arguments['user_id'] = user_id

                        # Log tool call
                        logger.info(f"Executing tool '{tool_name}' for user {user_id} with arguments: {arguments}")

                        # Create a simple object to mimic the expected interface
                        class MockToolCall:
                            def __init__(self, name, parameters):
                                self.name = name
                                self.parameters = parameters

                        tool_call_obj = MockToolCall(tool_name, arguments)
                        tool_result = await execute_tool_call(tool_call_obj, user_id)

                        # Log tool result
                        logger.info(f"Tool '{tool_name}' result for user {user_id}: success={tool_result.get('success', False)}")

                        tool_calls.append({
                            "name": tool_name,
                            "arguments": arguments,
                            "result": tool_result
                        })

                        tool_results.append(tool_result)

                    # Set response to the one provided in JSON, or create one based on tool results
                    # If there are error results, prioritize showing those error messages
                    error_results = [tr for tr in tool_results if not tr.get("success", True)]
                    if error_results:
                        logger.warning(f"Tool execution resulted in {len(error_results)} errors for user {user_id}")

                        # Combine error messages
                        error_messages = [tr.get("message", tr.get("error", "Unknown error")) for tr in error_results]
                        combined_error = " ".join(error_messages)
                        response_text = parsed_json.get("response", combined_error)
                    else:
                        logger.info(f"All tools executed successfully for user {user_id}")
                        response_text = parsed_json.get("response", f"Executed {len(tool_calls)} tool(s).")
                elif "response" in parsed_json:
                    # Just a plain response, no tools
                    response_text = parsed_json["response"]
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON response for user {user_id}: {response_text[:100]}...")
                # If JSON parsing fails, treat as regular text response
                pass

        logger.info(f"Returning response to user {user_id}: {response_text[:50]}...")
        return {
            "response": response_text,
            "tool_calls": tool_calls,
            "tool_results": tool_results
        }
    except Exception as e:
        logger.error(f"Error processing chat request for user {user_id}: {str(e)}", exc_info=True)

        # Return user-friendly error response
        error_msg = str(e)

        # Provide more helpful error messages based on common error types
        if "API" in error_msg.upper() or "COHERE" in error_msg.upper() or "AUTHENTICATION" in error_msg.upper():
            user_friendly_msg = "Sorry, I'm currently experiencing connectivity issues with the AI service. Please try again in a moment."
        elif "TIMEOUT" in error_msg.upper() or "CONNECTION" in error_msg.upper():
            user_friendly_msg = "Sorry, the connection to the AI service timed out. Please try your request again."
        else:
            user_friendly_msg = f"Sorry, I encountered an unexpected error: {str(e)[:100]}..." if len(str(e)) > 100 else f"Sorry, I encountered an error: {str(e)}"

        return {
            "response": user_friendly_msg,
            "tool_calls": [],
            "tool_results": [],
            "error": str(e)
        }


async def execute_tool_call(tool_call, user_id: str):
    """
    Execute a tool call and return the result
    This connects to the actual MCP tools
    """
    tool_name = tool_call.name
    params = tool_call.parameters

    logger.info(f"Executing tool '{tool_name}' for user {user_id} with parameters: {params}")

    # Add user_id to parameters if not already present
    if 'user_id' not in params:
        params['user_id'] = user_id

    # Import required classes at the beginning of the function to avoid scoping issues
    from mcp.tools.task_operations import (
        ListTasksParams, list_tasks_tool,
        CompleteTaskParams, complete_task_tool,
        DeleteTaskParams, delete_task_tool,
        UpdateTaskParams, update_task_tool
    )

    try:
        # Handle bulk operations first - if detected, return immediately
        if tool_name in ["complete_task", "delete_task", "update_task"]:
            # Check if the user wants to perform a bulk operation
            if 'task_id' in params and isinstance(params['task_id'], str):
                task_reference = params['task_id'].lower().strip()

                # Check for bulk operation keywords
                if task_reference in ['all', 'all tasks', 'every task', 'each task', 'all pending tasks']:
                    logger.info(f"Bulk operation detected: {tool_name} for all tasks for user {user_id}")

                    # Get all tasks for the user
                    list_params = ListTasksParams(user_id=user_id, status="all")
                    tasks_result = await list_tasks_tool(list_params)
                    all_tasks = tasks_result.get("tasks", [])

                    if not all_tasks:
                        return {
                            "success": True,
                            "message": "No tasks found to process.",
                            "bulk_operation": True,
                            "processed_count": 0
                        }

                    # Process each task individually
                    successful_count = 0
                    failed_tasks = []
                    failure_reasons = []

                    for task in all_tasks:
                        task_params = params.copy()
                        task_params['task_id'] = task['id']

                        # Execute the operation on this specific task
                        try:
                            if tool_name == "complete_task":
                                tool_params = CompleteTaskParams(**task_params)
                                result = await complete_task_tool(tool_params)
                            elif tool_name == "delete_task":
                                tool_params = DeleteTaskParams(**task_params)
                                result = await delete_task_tool(tool_params)
                            elif tool_name == "update_task":
                                tool_params = UpdateTaskParams(**task_params)
                                result = await update_task_tool(tool_params)

                            if result.get("success", False):
                                successful_count += 1
                            else:
                                failed_tasks.append(task)
                                failure_reasons.append(result.get("message", "Unknown error"))
                        except Exception as e:
                            logger.error(f"Failed to process task {task['id']} in bulk operation: {str(e)}")
                            failed_tasks.append(task)
                            failure_reasons.append(str(e))

                    return {
                        "success": True,
                        "message": f"Bulk operation completed. Successfully processed {successful_count} out of {len(all_tasks)} tasks." +
                                  (f" Failed to process {len(failed_tasks)} tasks." if failed_tasks else ""),
                        "bulk_operation": True,
                        "processed_count": successful_count,
                        "total_count": len(all_tasks),
                        "failed_count": len(failed_tasks),
                        "failure_reasons": failure_reasons
                    }

        # Handle task disambiguation for operations that require task identification
        if tool_name in ["complete_task", "delete_task", "update_task"]:
            # Check if the user provided a task reference (name, index, or ID)
            if 'task_id' in params and isinstance(params['task_id'], str):
                # Skip disambiguation if it's already a bulk operation keyword (handled above)
                task_reference = params['task_id'].lower().strip()
                if task_reference not in ['all', 'all tasks', 'every task', 'each task']:
                    logger.info(f"Attempting to resolve task reference '{params['task_id']}' to ID for user {user_id}")

                    # This might be a task name, index, or ID - try to resolve it
                    task_reference = params['task_id']

                    # Try to find the actual task by reference (name, index, or partial match)
                    resolved_task = await resolve_task_by_reference(task_reference, user_id)
                    if resolved_task:
                        logger.info(f"Resolved task reference '{task_reference}' to ID {resolved_task['id']} for user {user_id}")
                        params['task_id'] = resolved_task['id']
                    else:
                        # Find potential matches for clarification
                        potential_matches = await find_potential_task_matches(task_reference, user_id)
                        if potential_matches:
                            logger.info(f"Found {len(potential_matches)} potential matches for '{task_reference}' for user {user_id}")

                            if needs_clarification(task_reference, potential_matches):
                                # Need to ask user for clarification
                                task_list_str = "\n".join([f"- {task['title']} (ID: {task['id']})" for task in potential_matches])
                                logger.info(f"Requesting clarification for ambiguous task reference '{task_reference}' for user {user_id}")

                                return {
                                    "success": False,
                                    "error": "Ambiguous task reference",
                                    "message": f"I found multiple tasks matching '{task_reference}'. Please specify which one you mean:\n{task_list_str}"
                                }
                            else:
                                # Use the best match if it's clear
                                logger.info(f"Using best match for '{task_reference}': ID {potential_matches[0]['id']} for user {user_id}")
                                params['task_id'] = potential_matches[0]['id']
                        else:
                            # No matches found
                            logger.warning(f"No tasks found matching '{task_reference}' for user {user_id}")
                            return {
                                "success": False,
                                "error": "Task not found",
                                "message": f"I couldn't find a task matching '{task_reference}'. Please check the task name or list your tasks to see what's available."
                            }

        # Map tool names to actual functions and execute them (only if not a bulk operation)
        if tool_name == "add_task":
            tool_params = AddTaskParams(**params)
            logger.debug(f"Calling add_task_tool with params: {tool_params.__dict__}")
            result = await add_task_tool(tool_params)
        elif tool_name == "list_tasks":
            tool_params = ListTasksParams(**params)
            logger.debug(f"Calling list_tasks_tool with params: {tool_params.__dict__}")
            result = await list_tasks_tool(tool_params)
        elif tool_name == "complete_task":
            tool_params = CompleteTaskParams(**params)
            logger.debug(f"Calling complete_task_tool with params: {tool_params.__dict__}")
            result = await complete_task_tool(tool_params)
        elif tool_name == "delete_task":
            tool_params = DeleteTaskParams(**params)
            logger.debug(f"Calling delete_task_tool with params: {tool_params.__dict__}")
            result = await delete_task_tool(tool_params)
        elif tool_name == "update_task":
            tool_params = UpdateTaskParams(**params)
            logger.debug(f"Calling update_task_tool with params: {tool_params.__dict__}")
            result = await update_task_tool(tool_params)
        else:
            logger.error(f"Unknown tool called: {tool_name} for user {user_id}")
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "message": f"Unknown tool: {tool_name}"
            }

        # Handle cases where the operation failed due to non-existent task
        if not result.get("success", True):
            error_msg = result.get("error", "Unknown error")
            logger.warning(f"Tool '{tool_name}' failed for user {user_id}: {error_msg}")

            if "not found" in error_msg.lower() or "does not exist" in error_msg.lower() or "could not find" in error_msg.lower():
                task_id = params.get('task_id')
                if task_id:
                    result["message"] = f"I couldn't find a task with ID {task_id}. Please check the task ID or list your tasks to see what's available."
                else:
                    result["message"] = f"I couldn't complete the operation: {error_msg}"
        else:
            logger.info(f"Tool '{tool_name}' executed successfully for user {user_id}")

        return result
    except Exception as e:
        logger.error(f"Error executing tool '{tool_name}' for user {user_id}: {str(e)}", exc_info=True)

        # Handle unexpected errors during tool execution
        return {
            "success": False,
            "error": str(e),
            "message": f"An error occurred while executing the tool: {str(e)}"
        }


async def run_chat_agent_with_mcp(
    user_id: str,
    user_message: str,
    conversation_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Alternative implementation that connects to the MCP server directly
    """
    # This would be the real implementation that connects to the MCP server
    # For now, we'll use the Cohere-only approach above

    # Connect to MCP server
    # client = Client()
    # await client.connect("http://localhost:3000")  # MCP server endpoint

    # The actual implementation would:
    # 1. Prepare the message for the agent
    # 2. Provide the tools from the MCP server
    # 3. Process the response

    # For now, we'll call the simpler implementation
    return await run_chat_agent(user_id, user_message, conversation_history)