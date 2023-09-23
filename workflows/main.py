import os

from utils import File, Log

from osb_lk.ChatGPT import ChatGPT

log = Log('main')
ALL_LABEL = 'all'


def get_label(i: int):
    return f'part{i}'


def summary_lines():
    lines = []
    for i in range(0, 10):
        label = get_label(i)
        summary_path = os.path.join('ai_docs', f'{label}.summary.txt')
        lines += File(summary_path).read_lines()
    return lines


def process_part(i: int):
    log.info(f'Processing part {i}')
    part_file_path = os.path.join('docs', f'part{i}.txt')
    label = get_label(i)
    original_liens = File(part_file_path).read_lines()
    process_lines(label, original_liens)


def process_lines(label: str, original_lines: list[str]):
    story_ai = ChatGPT(original_lines)

    lines = []

    def print_x(line):
        print(line)
        lines.append(line)

    print_x(label)
    print_x(' ')
    print_x(story_ai.title)
    print_x(' ')
    print_x(story_ai.short_summary)
    print_x(' ')
    print_x('Summary')
    print_x(story_ai.summary)
    print_x(' ')

    summary_path = os.path.join('ai_docs', f'{label}.summary.txt')
    File(summary_path).write_lines(lines)
    log.info(f'Wrote {summary_path}')

    lines = []
    print_x(label)
    print_x(' ')
    print_x('Improvements')
    print_x(story_ai.improvements)
    print_x(' ')

    improvements_path = os.path.join('ai_docs', f'{label}.improvements.txt')
    File(improvements_path).write_lines(lines)
    log.info(f'Wrote {improvements_path}')


def build():
    for i in range(4, 10):
        process_part(i)
    process_lines(ALL_LABEL, summary_lines())


def paste():
    lines = []
    labels = [ALL_LABEL] + [get_label(i) for i in range(0, 10)]
    for label in labels:
        summary_path = os.path.join('ai_docs', f'{label}.summary.txt')
        lines += File(summary_path).read_lines()
        improvements_path = os.path.join(
            'ai_docs', f'{label}.improvements.txt'
        )
        lines += File(improvements_path).read_lines()
    complete_path = os.path.join('ai_docs', 'complete.txt')
    File(complete_path).write_lines(lines)
    log.info(f'Wrote {complete_path}')


def main():
    paste()


if __name__ == '__main__':
    main()
