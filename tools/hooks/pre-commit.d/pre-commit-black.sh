#!/bin/bash

# Copyright 2017-2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adapted from
# https://github.com/google/yapf/blob/d4933e857e85d2e685542d19d09282f59c12c6b4/plugins/pre-commit.sh
# (using black formatter instead of yapf)

# INSTALLING: This hook is only run by tox and does not need to be installed.
#
# Git pre-commit.d hook to check staged Python files for formatting issues with
# black.
#
# This requires that black is installed and runnable in the environment running
# the pre-commit.d hook.
#
# When running, this first checks for unstaged changes to staged files, and if
# there are any, it will exit with an error. Files with unstaged changes will be
# printed.
#
# If all staged files have no unstaged changes, it will run black against them,
# leaving the formatting changes unstaged. Changed files will be printed.
#
# BUGS: This does not leave staged changes alone when used with the -a flag to
# git commit, due to the fact that git stages ALL unstaged files when that flag
# is used.

# Find all staged Python files, and exit early if there aren't any.
PYTHON_FILES=(`git diff --name-only --cached --diff-filter=AM | \
  grep --color=never '.py$'`)
if [ ! "$PYTHON_FILES" ]; then
  exit 0
fi

# Verify that black is installed; if not, warn and exit.
if [ -z $(which black) ]; then
  echo 'black not on path; can not format. Please run using tox:'
  echo '    tox -e pre-commit-hooks'
  exit 2
fi

# Check for unstaged changes to files in the index.
CHANGED_FILES=(`git diff --name-only ${PYTHON_FILES[@]}`)
if [ "$CHANGED_FILES" ]; then
  echo 'You have unstaged changes to some files in your commit; skipping '
  echo 'auto-format. Please stage, stash, or revert these changes. You may '
  echo 'find `git stash -k` helpful here.'
  echo
  echo 'Files with unstaged changes:'
  for file in ${CHANGED_FILES[@]}; do
    echo "  $file"
  done
  exit 1
fi

# Format all staged files, then exit with an error code if any have uncommitted
# changes.
echo 'Formatting staged Python files . . .'
black ${PYTHON_FILES[@]}

CHANGED_FILES=(`git diff --name-only ${PYTHON_FILES[@]}`)
if [ "$CHANGED_FILES" ]; then
  echo 'Reformatted staged files. Please review and stage the changes.'
  echo
  echo 'Files updated:'
  for file in ${CHANGED_FILES[@]}; do
    echo "  $file"
  done
  exit 1
else
  exit 0
fi
