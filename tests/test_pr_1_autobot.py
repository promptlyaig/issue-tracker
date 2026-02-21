# Auto-generated tests by PR Review Bot
# Framework: pytest

import pytest

# Validates that the first page returns the correct set of items.
# Covers: pagination_bug
def test_paginate_first_page():
    items = list(range(25))
    paged_items = _paginate(items, 1, 10)
    assert paged_items == list(range(10))

# Validates that the second page returns the correct set of items.
# Covers: pagination_bug
def test_paginate_second_page():
    items = list(range(25))
    paged_items = _paginate(items, 2, 10)
    assert paged_items == list(range(10, 20))

# Validates filtering of issues by deportment ID.
# Covers: None
def test_filter_issues_by_deportment():
    issue1 = Issue(id='1', deportment_id='dep1', title='Issue 1')
    issue2 = Issue(id='2', deportment_id='dep2', title='Issue 2')
    issues['1'] = issue1
    issues['2'] = issue2
    filtered_issues = _filter_issues(deportment_id='dep1')
    assert len(filtered_issues) == 1
    assert filtered_issues[0].id == '1'
