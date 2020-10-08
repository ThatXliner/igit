import os

from git import Repo
from git import InvalidGitRepositoryError
from git import GitCommandError
from igit.interactive.display import Display


class GitOps:

    change_types = {
        'unstaged': None,
        'staged': 'HEAD'
    }

    def __init__(self, path=os.getcwd()) -> None:
        try:
            self.repo = Repo(path, search_parent_directories=True)
            self.repo_path = os.path.dirname(self.repo.git_dir)
            self.branch = self.repo.active_branch
            self.display = Display()

        except InvalidGitRepositoryError:
            raise InvalidGitRepositoryError('Not a git repo, I have no power here...')

    def get_changed_files(self, change):
        return [item.a_path for item in self.repo.index.diff(self.change_types[change])]

    def get_untracked_files(self):
        return self.repo.untracked_files

    def get_all_changes(self):
        return self.get_changed_files('staged') + \
               self.get_changed_files('unstaged') + \
               self.get_untracked_files()

    def calculate_change_list(self, diff_types=None):
        change_list = []
        for diff_type in diff_types:
            change_list += [item.a_path for item
                            in self.repo.index.diff(self.change_types[diff_type])]
        change_list += self.repo.untracked_files
        return change_list

    def switch_branch(self, branch_name):
        self.repo.git.checkout(branch_name)
        self.branch = self.repo.active_branch.name
        self.display.message(f'Switched to branch: {self.branch}', 'yellow', 'checkered_flag')


def in_gitignore(gitignore_path, item):
    gitignore = []
    with open(gitignore_path, 'r') as ignore_file:
        for line in ignore_file.readlines():
            gitignore.append(line.strip())
    return item in gitignore


def add_gitignore(gitignore_path, item):
    with open(gitignore_path, 'a') as ignore_file:
        ignore_file.write('\n')
        ignore_file.write(item)


if __name__ == '__main__':
    dir_path = '/Users/kobarhan/workspace/gitsy_test'
    gc = GitOps(dir_path)

    staged = gc.get_changed_files('staged')
    unstaged = gc.get_changed_files('unstaged')
    untracked = gc.get_untracked_files()

    print(f'staged changes: {staged}')
    print(f'unstaged changes: {unstaged}')
    print(f'untracked changes: {untracked}')

    print(f'all changes: {gc.get_all_changes()}')