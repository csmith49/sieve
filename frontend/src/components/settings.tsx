import { useState } from "react";

import { ArrowDown10, ArrowUp01, Ellipsis } from "lucide-react";
import { ThemeToggle } from "./theme-toggle";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "./ui/sheet";
import { Separator } from "./ui/separator";
import { Button } from "./ui/button";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "./ui/select";

function SortBehaviorItem() {
  const [sortStrategy, setSortStrategy] = useState<string>("date");
  const [sortDescending, setSortDescending] = useState<boolean>(true);

  return (
    <div className="flex flex-col gap-2">
      <div className="text-sm text-muted-foreground">
        Select the criteria by which papers are ordered.
      </div>
      <div className="flex gap-2">
        <Select defaultValue={sortStrategy} onValueChange={setSortStrategy}>
          <SelectTrigger className="w-[100%]">
            <SelectValue placeholder="Theme" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="date">Date</SelectItem>
            <SelectItem value="interest">Interest</SelectItem>
          </SelectContent>
        </Select>
        <Button
          variant="outline"
          onClick={() => setSortDescending(!sortDescending)}
        >
          {sortDescending ? <ArrowDown10 /> : <ArrowUp01 />}
        </Button>
      </div>
    </div>
  );
}

function ForceDataUpdateItem() {
  return (
    <div className="flex flex-col gap-2">
      <div className="text-sm text-muted-foreground">
        Force the backend to query arXiv for any newly-published papers.
      </div>
      <Button>Force data update</Button>
    </div>
  );
}

export function Settings(props: {}) {
  return (
    <Sheet>
      <SheetTrigger>
        <Button variant="ghost">
          <Ellipsis />
        </Button>
      </SheetTrigger>
      <SheetContent className="flex flex-col">
        <SheetHeader>
          <SheetTitle>Settings</SheetTitle>
          <SheetDescription>
            Configure the appearance and behavior of Sieve.
          </SheetDescription>
        </SheetHeader>
        <Separator />
        <div className="flex flex-col gap-2">
          <div>Data</div>
          <SortBehaviorItem />
          <ForceDataUpdateItem />
        </div>
        <Separator />
        <div className="flex flex-col gap-2">
          <div>Theme</div>
          <div className="text-sm text-muted-foreground">
            Change how Sieve provides contrast between the information and the
            background.
          </div>
          <ThemeToggle />
        </div>
        <div className="grow" />
        <SheetFooter>Copyright Calvin Smith 2024.</SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
