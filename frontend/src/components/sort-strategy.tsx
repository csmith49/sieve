import { useEffect, useState } from "react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
  SelectGroup,
} from "./ui/select";

export type SortStrategy = {
  sort_kind: string;
  sort_direction: string;
};

function SortStrategySelection(props: {
  onSortStrategyChange?: (strategy: SortStrategy) => void;
}) {
  const [selection, setSelection] = useState<string>("most recent");

  function setStrategy(strategy: SortStrategy) {
    if (props.onSortStrategyChange) {
      props.onSortStrategyChange(strategy);
    }
  }

  useEffect(() => {
    switch (selection) {
      case "most recent":
        setStrategy({ sort_kind: "date", sort_direction: "descending" });
        break;

      case "least recent":
        setStrategy({ sort_kind: "date", sort_direction: "ascending" });
        break;

      case "most interested":
        setStrategy({ sort_kind: "interest", sort_direction: "descending" });
        break;

      case "least interested":
        setStrategy({ sort_kind: "interest", sort_direction: "ascending" });
        break;
    }
  }, [selection]);

  return (
    <Select defaultValue="most recent" onValueChange={setSelection}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Sort by" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectItem value="most recent">Most recent</SelectItem>
          <SelectItem value="least recent">Least recent</SelectItem>
          <SelectItem value="most interested">Most interested</SelectItem>
          <SelectItem value="least interested">Least interested</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}

export default SortStrategySelection;
