import pytest

from pattern import Pattern


@pytest.mark.parametrize('s,p,result',
                         [
                             ["aa", "a", False],
                             ["abc", "ab", False],
                             ["abc", "abc", True],
                             ["a", ".", True],
                             ["aa", ".", False],
                             ["aa", "a*", True],
                             ["aa", "a*a", True],
                             ["aac", "a*c", True],
                             ["aacb", "a*cb", True],
                             ["aac", "a*c*", True],
                             ["aacc", "a*c*", True],
                             ["ab", ".*", True],
                             ["aab", "c*a*b", True],
                             ["ab", ".*c", False],
                             ["aaa", "a*a", True],
                             ["aaa", "a*aa", True],
                             ["mississippi", "mis*is*p*.", False],
                             ["aaa", "ab*a", False],
                             ["a", "ab*", True],
                             ["a", ".*..a*", False],
                             ["aaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*c", False],
                             ["aba", ".*.*", True],
                             ["aaaaaaaaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*a*", False],
                          ])
def test_is_match(s, p, result):
    patt = Pattern(p)
    assert patt.match(s) is result
