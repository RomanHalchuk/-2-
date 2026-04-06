class SimplifiedMarkdownEditor:
    def __init__(self):
        self.result = ""
        self.formatters = {
            "plain",
            "bold",
            "italic",
            "header",
            "link",
            "inline-code",
            "ordered-list",
            "unordered-list",
            "new-line"
        }
        self.special_commands = {"!help", "!done", "exit"}

    def print_help(self):
        print("Available formatters: plain bold italic header link inline-code "
              "ordered-list unordered-list new-line")
        print("Special commands: !help !done")

    def get_rows(self):
        while True:
            try:
                rows = int(input("Number of rows: > "))
                if rows <= 0:
                    print("The number of rows should be greater than zero")
                else:
                    return rows
            except ValueError:
                print("The number of rows should be greater than zero")

    def run(self):
        print("Hi User! This is Simplified Markdown_Editor.\n"
             "Formatter: plain, bold, italic ,header, link, inline-code, ordered-list, unordered-list, new-line.\n"
              "Special commands: !help, !done, exit.")
        while True:
            formatter = input("Choose a formatter:\n> ")

            if formatter in self.special_commands:
                if formatter == "!help":
                    self.print_help()
                elif formatter == "!done":
                    with open("output.md", "w", encoding="utf-8") as f:
                        f.write(self.result)
                    print("Markdown saved to output.md. Exiting.")
                    break
                elif formatter == "exit":
                    print("Exiting without saving.")
                    break
                continue

            if formatter not in self.formatters:
                print("Unknown formatting type or command")
                continue

            if formatter == "plain":
                text = input("Text: > ")
                self.result += text

            elif formatter == "bold":
                text = input("Text: > ")
                self.result += f"**{text}**"

            elif formatter == "italic":
                text = input("Text: > ")
                self.result += f"*{text}*"

            elif formatter == "inline-code":
                text = input("Text: > ")
                self.result += f"`{text}`"

            elif formatter == "header":
                while True:
                    try:
                        level = int(input("Level: > "))
                        if 1 <= level <= 6:
                            break
                        else:
                            print("The level should be within the range of 1 to 6")
                    except ValueError:
                        print("The level should be within the range of 1 to 6")
                text = input("Text: > ")
                self.result += f"{'#' * level} {text}\n"

            elif formatter == "link":
                label = input("Label: > ")
                url = input("URL: > ")
                self.result += f"[{label}]({url})"


            elif formatter == "new-line":
                if self.result.endswith("\n\n"):
                    pass
                elif self.result.endswith("\n"):
                    self.result += "\n"
                else:
                    self.result += "\n\n"

            elif formatter == "ordered-list":
                rows = self.get_rows()
                if self.result and not self.result.endswith("\n"):
                    self.result += "\n"

                for i in range(1, rows + 1):
                    row = input(f"Row #{i}: > ")
                    self.result += f"{i}. {row}\n"
                self.result += "\n"

            elif formatter == "unordered-list":

                rows = self.get_rows()

                if self.result and not self.result.endswith("\n"):
                    self.result += "\n"

                for i in range(1, rows + 1):
                    row = input(f"Row #{i}: > ")

                    self.result += f"* {row}\n"

                self.result += "\n"

            print(self.result)


if __name__ == "__main__":
    editor = SimplifiedMarkdownEditor()
    editor.run()