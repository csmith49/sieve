import "./App.css";
import { useEffect, useState } from "react";

import SortStrategySelection, {
  SortStrategy,
} from "./components/sort-strategy";
import FilterStrategySelection, {
  FilterStrategy,
} from "./components/filter-strategy";
import { PaperList } from "./components/paper";

function App() {
  const [sortStrategy, setSortStrategy] = useState<SortStrategy>({
    sort_kind: "date",
    sort_direction: "descending",
  });
  const [filterStrategy, setFilterStrategy] = useState<FilterStrategy>({
    filters: [],
  });
  const [papers, setPapers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/papers")
      .then((response) => response.json())
      .then(setPapers)
      .catch((error) => console.error("Error fetching data: ", error));
  }, [sortStrategy, filterStrategy]);

  return (
    <div>
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <div className="text-lg">sieve</div>
        <div className="grow"></div>
        <SortStrategySelection onSortStrategyChange={setSortStrategy} />
        <FilterStrategySelection onFilterStrategyChange={setFilterStrategy} />
      </header>
      <div className="flex flex-1 flex-col gap-4 p-4">
        <PaperList papers={papers} />
      </div>
    </div>
  );
}
export default App;
