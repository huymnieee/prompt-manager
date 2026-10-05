"""실제 콘솔 프로그램을 실행하여 사용 흐름과 오류 처리를 검증한다."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent


class PromptManagerTests(unittest.TestCase):
    def run_app(self, inputs, empty=False):
        command = [sys.executable, str(ROOT / 'main.py')]
        if empty:
            command = [sys.executable, '-c', 'import main; main.prompts = []; main.main()']
        result = subprocess.run(command, input=inputs, text=True, capture_output=True, cwd=ROOT, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        return result.stdout

    def test_menu_repeats_and_invalid_menu_recovers(self):
        output = self.run_app('oops\n99\n2\n0\n')
        self.assertEqual(output.count('=== 나만의 프롬프트 관리 ==='), 4)
        self.assertEqual(output.count('잘못된 메뉴 번호입니다'), 2)
        self.assertIn('총 4개의 프롬프트', output)
        self.assertIn('프로그램을 종료합니다', output)

    def test_add_retries_empty_fields_and_invalid_category(self):
        output = self.run_app('1\n \n테스트 제목\n\n테스트 내용\n잘못\n0\n7\n5\n2\n5\n5\n0\n')
        self.assertEqual(output.count('빈 내용은 입력할 수 없습니다'), 2)
        self.assertEqual(output.count('잘못된 카테고리 번호입니다'), 3)
        self.assertIn('5. [자동화] 테스트 제목', output)
        self.assertIn('내용:\n테스트 내용', output)
        self.assertIn('즐겨찾기: 없음', output)

    def test_category_uses_original_numbers_and_handles_empty_result(self):
        output = self.run_app('3\n3\n3\n2\n0\n')
        self.assertIn('3. [영상 생성] Dream X 광고 씬1 생성', output)
        self.assertIn('4. [영상 생성] Dream X 한강 버스킹 씬2 생성', output)
        self.assertIn('총 2개의 프롬프트', output)
        self.assertIn('표시할 프롬프트가 없습니다', output)

    def test_search_finds_content_case_insensitively_and_recovers(self):
        output = self.run_app('4\n \n흥얼\n4\ndream x\n4\n없는검색어xyz\n0\n')
        self.assertIn('빈 내용은 입력할 수 없습니다', output)
        self.assertIn('3. [영상 생성] Dream X 광고 씬1 생성', output)
        self.assertIn('총 2개의 프롬프트', output)
        self.assertIn('검색 결과가 없습니다', output)

    def test_detail_rejects_invalid_numbers_and_shows_entire_content(self):
        output = self.run_app('5\nabc\n5\n0\n5\n-1\n5\n999\n5\n3\n0\n')
        self.assertEqual(output.count('잘못된 번호입니다'), 4)
        self.assertIn('제목: Dream X 광고 씬1 생성', output)
        self.assertIn('마지막에는 아쉬운 표정을 짓는다. 세로형 영상.', output)

    def test_favorites_toggle_and_filtered_numbers_remain_consistent(self):
        output = self.run_app('7\n6\n3\n7\n5\n3\n6\n3\n7\n0\n')
        self.assertEqual(output.count('즐겨찾기한 프롬프트가 없습니다'), 2)
        self.assertIn('즐겨찾기를 추가했습니다', output)
        self.assertIn('3. [영상 생성] Dream X 광고 씬1 생성 ⭐', output)
        self.assertIn('즐겨찾기: ⭐', output)
        self.assertIn('즐겨찾기를 해제했습니다', output)

    def test_empty_prompt_list_is_safe(self):
        output = self.run_app('2\n3\n1\n4\n아무거나\n5\n6\n7\n0\n', empty=True)
        self.assertIn('표시할 프롬프트가 없습니다', output)
        self.assertEqual(output.count('등록된 프롬프트가 없습니다'), 2)
        self.assertIn('검색 결과가 없습니다', output)
        self.assertIn('즐겨찾기한 프롬프트가 없습니다', output)

    def test_added_data_resets_when_restarted(self):
        self.run_app('1\n임시 데이터\n잠깐만 유지\n6\n6\n5\n0\n')
        output = self.run_app('2\n7\n0\n')
        self.assertIn('총 4개의 프롬프트', output)
        self.assertNotIn('임시 데이터', output)
        self.assertIn('즐겨찾기한 프롬프트가 없습니다', output)

    def test_end_of_input_exits_gracefully(self):
        for inputs in ['', '1\n', '1\n제목\n내용\n', '5\n']:
            with self.subTest(inputs=inputs):
                self.assertIn('입력이 끝나 프로그램을 종료합니다', self.run_app(inputs))

    def test_import_does_not_start_interactive_menu(self):
        result = subprocess.run([sys.executable, '-c', 'import main'], cwd=ROOT, text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')

    def test_edit_updates_all_fields_and_preserves_favorite(self):
        output = self.run_app('6\n1\n8\n1\n\n새 코치\n \n새 설명\n0\n5\n5\n1\n7\n0\n')
        self.assertIn('프롬프트를 수정했습니다', output)
        self.assertIn('제목: 새 코치', output)
        self.assertIn('카테고리: 자동화', output)
        self.assertIn('내용:\n새 설명', output)
        self.assertIn('1. [자동화] 새 코치 ⭐', output)
        self.assertEqual(output.count('빈 내용은 입력할 수 없습니다'), 2)

    def test_delete_cancel_then_confirm_reindexes_items(self):
        output = self.run_app('9\n1\nn\n2\n9\n1\ny\n2\n5\n1\n0\n')
        self.assertIn('삭제를 취소했습니다', output)
        self.assertIn('총 4개의 프롬프트', output)
        self.assertIn('프롬프트를 삭제했습니다', output)
        self.assertIn('총 3개의 프롬프트', output)
        self.assertIn('1. [텍스트 생성] 다이어트 고민 답변 생성', output)

    def test_edit_delete_empty_and_invalid_selection_are_safe(self):
        output = self.run_app('8\n-1\n9\nabc\n0\n')
        self.assertEqual(output.count('잘못된 번호입니다'), 2)
        output = self.run_app('8\n9\n0\n', empty=True)
        self.assertEqual(output.count('등록된 프롬프트가 없습니다'), 2)

    def test_delete_only_selected_duplicate_and_reset_on_restart(self):
        output = self.run_app('1\n동일 제목\n동일 내용\n6\n1\n동일 제목\n동일 내용\n6\n6\n6\n9\n6\ny\n7\n2\n0\n')
        self.assertIn('총 5개의 프롬프트', output)
        self.assertIn('5. [기타] 동일 제목', output)
        self.assertIn('즐겨찾기한 프롬프트가 없습니다', output)
        self.assertNotIn('5. [기타] 동일 제목 ⭐', output)
        self.assertIn('총 4개의 프롬프트', self.run_app('2\n0\n'))


if __name__ == '__main__':
    unittest.main()
