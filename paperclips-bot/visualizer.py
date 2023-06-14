import curses
from enum import Enum

from history import TO_TRACK


class VisualizerState(Enum):
    RUN = 1
    QUIT = 2


class Visualizer:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.screen.nodelay(True)

    def draw(self, history) -> VisualizerState:
        if self.screen.getch() == ord("q"):
            return VisualizerState.QUIT

        self.screen.clear()

        self.screen.addstr(f"Tick: {history.tick_num}\n\n")

        cw = [12, 10, 10, 7]  # Column widths
        self.screen.addstr("Name\t".rjust(cw[0]))
        self.screen.addstr("Total\t".rjust(cw[1]))
        self.screen.addstr("Trend\t".rjust(cw[2]))
        self.screen.addstr("Trend (%)\t".rjust(cw[3]))
        self.screen.addstr("\n")

        self.screen.addstr(
            "-" * (sum(cw) + len(cw) * (len("\t".expandtabs()) - 1)) + "\n"
        )

        if len(history) > 0:
            for data in TO_TRACK:
                name = data.name
                current = history[name][-1]
                trend_real = history.trend_real[name]
                trend_percent = history.trend_percent[name]

                if current == 0 and trend_real == 0 and trend_percent == 0:
                    continue

                try:
                    self.screen.addstr(f"{name}\t".rjust(cw[0]))
                    self.screen.addstr(
                        f"{Visualizer.limit_num_str(current, cw[1])}\t".rjust(
                            cw[1]
                        )
                    )
                    self.screen.addstr(
                        f"{Visualizer.limit_num_str(trend_real, cw[2])}\t".rjust(
                            cw[2]
                        )
                    )
                    self.screen.addstr(
                        f"{(100 * trend_percent):.3f}\n".rjust(cw[3])
                    )
                except:
                    break

        self.screen.refresh()

        return VisualizerState.RUN

    def return_terminal_state(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def limit_num_str(num, max_len):
        if len(str(num)) > max_len:
            return f"{num:e}"
        else:
            return str(num)
