import os

from utils import File, Log

from osb_lk.ChatGPT import ChatGPT

log = Log('main')


def process_part(i: int):
    log.info(f'Processing part {i}')
    part_file_path = os.path.join('docs', f'part{i}.txt')
    story_ai = ChatGPT(File(part_file_path).read_lines())

    lines = []

    def print_x(line):
        print(line)
        lines.append(line)

    print_x(f'Part {i}')
    print_x(' ')
    print_x(story_ai.title)
    print_x(' ')
    print_x(story_ai.short_summary)
    print_x(' ')
    print_x('Summary')
    print_x(story_ai.summary)
    print_x(' ')

    summary_path = os.path.join('ai_docs', f'part{i}.summary.txt')
    File(summary_path).write_lines(lines)
    log.info(f'Wrote {summary_path}')

    lines = []
    print_x(f'Part {i}')
    print_x(' ')
    print_x('Improvements')
    print_x(story_ai.improvements)
    print_x(' ')

    improvements_path = os.path.join('ai_docs', f'part{i}.improvements.txt')
    File(improvements_path).write_lines(lines)
    log.info(f'Wrote {improvements_path}')


def main():
    for i in range(4, 10):
        process_part(i)


if __name__ == '__main__':
    main()
