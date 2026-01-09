export default function Footer() {
  return (
    <footer className="bg-black py-6">
      <div className="container mx-auto px-4 text-center text-white">
        <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
      </div>
    </footer>
  );
}