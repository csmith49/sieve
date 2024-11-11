import { useEffect, useState } from "react";

import { Switch } from "./ui/switch";
import { Skeleton } from "./ui/skeleton";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "./ui/collapsible";
import { Table, TableBody, TableCell, TableRow } from "./ui/table";
import { ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "./ui/button";

export type Paper = {
  id: string;
  title: string;
  interest: boolean;
  abstract: string;
  authors: string[];
  categories: string[];
};

export function RenderPaper(props: {
  id: string;
  render: (paper: Paper) => JSX.Element;
}): JSX.Element {
  const [paper, setPaper] = useState<Paper | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/paper/" + props.id)
      .then((response) => response.json())
      .then(setPaper)
      .catch((error) => console.error("Cannot fetch paper: ", error));
  }, []);

  return paper ? (
    props.render(paper)
  ) : (
    <Skeleton className="h-[100px] w-[100%]" />
  );
}

export function InterestSelector(props: { paper: Paper }) {
  const [interest, setInterest] = useState<boolean>(props.paper.interest);

  const handleInterestChange = () => {
    fetch("http://127.0.0.1:8000/interest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: props.paper.id, interest: !interest }),
    });
    setInterest(!interest);
  };

  return <Switch checked={interest} onCheckedChange={handleInterestChange} />;
}

export function PaperSource(props: { paper: Paper }) {
  return (
    <a
      href={"https://arxiv.org/pdf/" + props.paper.id}
      target="_blank"
      className="text-sm text-muted-foreground"
    >
      {props.paper.id}
    </a>
  );
}

export function PaperDetailsTable(props: { paper: Paper }) {
  return (
    <Table>
      <TableBody>
        <TableRow key="details-authors">
          <TableCell className="align-text-top text-right text-sm text-muted-foreground">
            authors
          </TableCell>
          <TableCell>{props.paper.authors.join(", ")}</TableCell>
        </TableRow>
        <TableRow key="details-abstract">
          <TableCell className="align-text-top text-right text-sm text-muted-foreground">
            abstract
          </TableCell>
          <TableCell className="whitespace-pre-line">
            <p>{props.paper.abstract}</p>
          </TableCell>
        </TableRow>
        <TableRow key="details-categories">
          <TableCell className="align-text-top text-right text-sm text-muted-foreground">
            categories
          </TableCell>
          <TableCell>{props.paper.categories.join(", ")}</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
}

function PaperListItem(props: { paper: Paper }) {
  const [detailsVisible, setDetailsVisible] = useState<boolean>(false);
  return (
    <li key={props.paper.id} className="pb-4 border-b-2">
      <Collapsible
        className="w-[100%]"
        open={detailsVisible}
        onOpenChange={setDetailsVisible}
      >
        <div className="flex gap-4">
          <InterestSelector paper={props.paper} />
          <div className="w-[100%]">
            <div className="flex w-[100%]">
              <div className="grow">
                <div>{props.paper.title}</div>
                <PaperSource paper={props.paper} />
              </div>
              <CollapsibleTrigger className="grow-0">
                <Button variant="ghost">
                  {!detailsVisible ? <ChevronDown /> : <ChevronUp />}
                </Button>
                {/* <div className="align-text-top h-[100%] text-muted-foreground">
                </div> */}
              </CollapsibleTrigger>
            </div>
            <CollapsibleContent>
              <PaperDetailsTable paper={props.paper} />
            </CollapsibleContent>
          </div>
        </div>
      </Collapsible>
    </li>
  );
}

export function PaperList(props: { papers: string[] }) {
  return (
    <ol className="space-y-4">
      {props.papers.map((id) => (
        <RenderPaper
          id={id}
          render={(paper) => <PaperListItem paper={paper} />}
        />
      ))}
    </ol>
  );
}

export function PaperCard(props: { id: string }) {
  return (
    <RenderPaper
      id={props.id}
      render={(paper) => (
        <div>
          <div>{paper.title}</div>
          <div>{paper.authors}</div>
          <div>{paper.abstract}</div>
          <InterestSelector paper={paper} />
        </div>
      )}
    />
  );
}
