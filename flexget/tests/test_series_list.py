from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin


class TestListInterface(object):
    config = """
        templates:
          global:
            disable: [seen]
            metainfo_series: yes

        tasks:
          list_get:
            series_list: test_list

          list_1_get:
            series_list: list 1

          list_2_get:
            series_list: list 2

          test_list_add:
            mock:
              - {title: 'Some.Series.S01E20.720p.XViD-FlexGet', url: "http://mock.url/file1.torrent"}
              - {title: 'Other.Series.S01E20.720p-FlexGet', url: "http://mock.url/file2.torrent"}
            accept_all: yes
            list_add:
              - series_list: test_list

          list_1_add:
            mock:
              - {title: 'Some.Series.S01E20.720p.XViD-FlexGet', url: "http://mock.url/file1.torrent"}
              - {title: 'Other.Series.S01E20.720p-FlexGet', url: "http://mock.url/file2.torrent"}
            accept_all: yes
            list_add:
              - series_list: list 1

          list_2_add:
            mock:
              - {title: 'title 3', url: "http://mock.url/file3.torrent"}
            accept_all: yes
            list_add:
              - series_list: list 2

          test_multiple_list_add:
            mock:
              - {title: 'Some.Series.S01E20.720p.XViD-FlexGet', url: "http://mock.url/file1.torrent"}
              - {title: 'Other.Series.S01E20.720p-FlexGet', url: "http://mock.url/file2.torrent"}
            accept_all: yes
            list_add:
              - series_list: list 1
              - series_list: list 2

          test_list_accept_with_remove:
            mock:
              - {title: 'title 1', url: "http://mock.url/file1.torrent"}
              - {title: 'title 2', url: "http://mock.url/file2.torrent"}
              - {title: 'title 3', url: "http://mock.url/file3.torrent"}
            list_match:
              from:
                - series_list: test_list

          test_list_accept_without_remove:
            mock:
              - {title: 'title 1', url: "http://mock.url/file1.torrent"}
              - {title: 'title 2', url: "http://mock.url/file2.torrent"}
              - {title: 'title 3', url: "http://mock.url/file3.torrent"}
            list_match:
              from:
                - series_list: test_list
              remove_on_match: no

          test_multiple_list_accept_with_remove:
            mock:
              - {title: 'title 1', url: "http://mock.url/file1.torrent"}
              - {title: 'title 2', url: "http://mock.url/file2.torrent"}
              - {title: 'title 3', url: "http://mock.url/file3.torrent"}
            list_match:
              from:
                - series_list: list 1
                - series_list: list 2

          test_multiple_list_accept_without_remove:
            mock:
              - {title: 'title 1', url: "http://mock.url/file1.torrent"}
              - {title: 'title 2', url: "http://mock.url/file2.torrent"}
              - {title: 'title 3', url: "http://mock.url/file3.torrent"}
            list_match:
              from:
                - series_list: list 1
                - series_list: list 2
              remove_on_match: no

          test_list_remove:
            mock:
              - {title: 'title 1', url: "http://mock.url/file1.torrent"}
            accept_all: yes
            list_remove:
              - series_list: test_list

          test_list_reject:
            mock:
              - {title: 'title 1', url: "http://mock.url/file1.torrent"}
              - {title: 'title 3', url: "http://mock.url/file3.torrent"}
            list_match:
              from:
                - series_list: test_list
              action: reject

          test_allowed_identifiers:
            mock:
              - {title: 'title 1',
                 url: "http://mock.url/file1.torrent",
                 imdb_id: "tt1234567",
                 trakt_movie_id: "12345",
                 tmdb_id: "3456",
                 fake_id_name: "123abc"
                 }
            accept_all: yes
            list_add:
              - series_list: test_list

          test_list_accept_for_real_title:
            mock:
              - {title: 'title.1.720p.BluRay.x264-Group'}
            list_match:
              from:
                - series_list: test_list
    """

    def test_list_add(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.entries) == 2

        task = execute_task('list_get')
        assert len(task.entries) == 2

    def test_multiple_list_add(self, execute_task):
        task = execute_task('test_multiple_list_add')
        assert len(task.entries) == 2

        task = execute_task('list_1_get')
        assert len(task.entries) == 2

        task = execute_task('list_2_get')
        assert len(task.entries) == 2

    def test_list_accept_with_remove(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.entries) == 2

        task = execute_task('list_get')
        assert len(task.entries) == 2

        task = execute_task('test_list_accept_with_remove')
        assert len(task.all_entries) == 3
        assert len(task.accepted) == 2

        task = execute_task('list_get')
        assert len(task.entries) == 0

    def test_list_accept_without_remove(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.entries) == 2

        task = execute_task('list_get')
        assert len(task.entries) == 2

        task = execute_task('test_list_accept_without_remove')
        assert len(task.all_entries) == 3
        assert len(task.accepted) == 2

        task = execute_task('list_get')
        assert len(task.entries) == 2

    def test_multiple_list_accept_with_remove(self, execute_task):
        task = execute_task('list_1_add')
        assert len(task.entries) == 2

        task = execute_task('list_2_add')
        assert len(task.entries) == 1

        task = execute_task('list_1_get')
        assert len(task.entries) == 2

        task = execute_task('list_2_get')
        assert len(task.entries) == 1

        task = execute_task('test_multiple_list_accept_with_remove')
        assert len(task.accepted) == 3

        task = execute_task('list_1_get')
        assert len(task.entries) == 0

        task = execute_task('list_2_get')
        assert len(task.entries) == 0

    def test_multiple_list_accept_without_remove(self, execute_task):
        task = execute_task('list_1_add')
        assert len(task.entries) == 2

        task = execute_task('list_2_add')
        assert len(task.entries) == 1

        task = execute_task('list_1_get')
        assert len(task.entries) == 2

        task = execute_task('list_2_get')
        assert len(task.entries) == 1

        task = execute_task('test_multiple_list_accept_without_remove')
        assert len(task.accepted) == 3

        task = execute_task('list_1_get')
        assert len(task.entries) == 2

        task = execute_task('list_2_get')
        assert len(task.entries) == 1

    def test_list_remove(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.entries) == 2

        task = execute_task('list_get')
        assert len(task.entries) == 2

        task = execute_task('test_list_remove')
        assert len(task.accepted) == 1

        task = execute_task('list_get')
        assert len(task.entries) == 1

    def test_list_reject(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.entries) == 2

        task = execute_task('list_get')
        assert len(task.entries) == 2

        task = execute_task('test_list_reject')
        assert len(task.rejected) == 1

    def test_list_accept_for_real_title(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.entries) == 2

        task = execute_task('test_list_accept_for_real_title')
        assert len(task.accepted) == 1
