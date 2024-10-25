import { useEffect, useState } from "react";
import { ToggleGroup, ToggleGroupItem } from "./ui/toggle-group";

export type FilterStrategy = {
  filters: string[];
};

function FilterStrategySelection(props: {
  onFilterStrategyChange?: (strategy: FilterStrategy) => void;
}) {
  const [filters, setFilters] = useState<string[]>([]);

  useEffect(() => {
    if (props.onFilterStrategyChange) {
      props.onFilterStrategyChange({ filters: filters });
    }
  }, [filters]);

  return (
    <ToggleGroup type="multiple" onValueChange={setFilters}>
      <ToggleGroupItem value="today" aria-label="Toggle filter today">
        Today
      </ToggleGroupItem>
      <ToggleGroupItem value="interested" aria-label="Toggle filter interested">
        Interested
      </ToggleGroupItem>
    </ToggleGroup>
  );
}
export default FilterStrategySelection;
