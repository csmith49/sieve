import { useEffect, useState } from "react";

import { Button } from "./components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "./components/ui/card";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "./components/ui/collapsible";
import { Separator } from "./components/ui/separator";
import { AppSidebar } from "./components/app-sidebar";
import {
  SidebarProvider,
  SidebarInset,
  SidebarTrigger,
} from "./components/ui/sidebar";
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbSeparator,
  BreadcrumbPage,
} from "./components/ui/breadcrumb";

import "./App.css";

type PaperData = {
  id: string;
  title: string;
  interest: boolean;
  abstract: string;
};

function Paper(props: { id: string }) {
  const [data, setData] = useState<PaperData | null>(null);
  const [isLiked, setIsLiked] = useState<Boolean>(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/paper/" + props.id)
      .then((response) => response.json())
      .then(setData)
      .catch((error) => console.error("Cannot fetch paper: ", error));
  }, []);

  useEffect(() => {
    if (data) {
      setIsLiked(data.interest);
    }
  }, [data]);

  const handleLiked = () => {
    fetch("http://127.0.0.1:8000/interest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: props.id, interest: !isLiked }),
    });
    setIsLiked(!isLiked);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{data?.title}</CardTitle>
      </CardHeader>
      <Separator />
      <CardContent>
        <Collapsible>
          <CollapsibleTrigger>
            <p>abstract</p>
          </CollapsibleTrigger>
          <CollapsibleContent>{data?.abstract}</CollapsibleContent>
        </Collapsible>
      </CardContent>
      <CardFooter>
        <Button onClick={handleLiked}>{isLiked ? "YES" : "NO"}</Button>
      </CardFooter>
    </Card>
  );
}

function App() {
  const [papers, setPapers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/papers")
      // .then((response) => console.log(response))
      .then((response) => response.json())
      .then(setPapers)
      .catch((error) => console.error("Error fetching data: ", error));
  }, []);

  const activePapers = papers.slice(0, 10);

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem className="hidden md:block">
                <BreadcrumbLink href="#">
                  Building Your Application
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator className="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Data Fetching</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4">
          {activePapers.map((paperId) => (
            <Paper key={paperId} id={paperId} />
          ))}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
export default App;
