import { useEffect, useState } from "react";
import {
  Typography,
  Button,
  Card,
  List,
  ListItem,
  CardActions,
} from "@mui/joy";
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
      <Typography level="h3">{data?.title}</Typography>
      <Typography>{data?.abstract}</Typography>
      <CardActions>
        <Button onClick={handleLiked}>{isLiked ? "YES" : "NO"}</Button>
      </CardActions>
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
    <div>
      <List>
        {activePapers.map((paperId) => (
          <ListItem key={paperId}>
            <Paper id={paperId} />
          </ListItem>
        ))}
      </List>
    </div>
  );
}

export default App;
