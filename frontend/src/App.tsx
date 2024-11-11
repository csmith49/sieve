import "./App.css";
import { ThemeProvider } from "./components/theme-provider";
import { useEffect, useState } from "react";

import { PaperList } from "./components/paper";

import { Settings } from "./components/settings";

function App() {
  const [papers, setPapers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/papers")
      .then((response) => response.json())
      .then(setPapers)
      .catch((error) => console.error("Error fetching data: ", error));
  }, []);

  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <div className="text-lg">sieve</div>
        <div className="grow"></div>
        <Settings />
      </header>
      <div className="flex flex-1 flex-col gap-4 p-4">
        <PaperList papers={papers} />
      </div>
    </ThemeProvider>
  );
}
export default App;
