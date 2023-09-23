import os

from utils import File, Log

from osb_lk.ChatGPT import ChatGPT

log = Log('main')


def process_part(i: int):
    log.info(f'Processing part {i}')
    part_file_path = os.path.join('docs', f'part{i}.txt')
    story_ai = ChatGPT(File(part_file_path).read_lines())

    lines = [f'Part {i}']
    lines.append(story_ai.title)
    lines.append(story_ai.summary)

    summary_path = os.path.join('ai_docs', f'summary.part{i}.txt')
    File(summary_path).write_lines(lines)
    log.info(f'Wrote {summary_path}')


def main():
    for i in range(0, 1):
        process_part(i)


if __name__ == '__main__':
    main()
