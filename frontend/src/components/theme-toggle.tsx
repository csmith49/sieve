import { useTheme } from "@/components/theme-provider";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "./ui/select";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Select defaultValue={theme} onValueChange={setTheme}>
      <SelectTrigger className="w-[100%]">
        <SelectValue placeholder="Theme" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="light">Light</SelectItem>
        <SelectItem value="dark">Dark</SelectItem>
        <SelectItem value="system">System</SelectItem>
      </SelectContent>
    </Select>
  );
}
