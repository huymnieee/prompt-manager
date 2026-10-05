"""이전 AI 과제의 프롬프트를 관리하는 콘솔 프로그램."""

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

prompts = [
    {
        "title": "다이어트 멘탈 코치 페르소나",
        "content": "말투는 다정하고 친절한 1:1 다이어트 전문가 친구 같은 느낌으로 유지해줘. 행동 대안은 마음이 힘든 지금 상황에서 내일 당장 쉽게 접근할 수 있는 만만하고 구체적인 내용으로 알려줘. 대안은 1, 2, 3 번호를 매겨서 가독성 있게 작성해줘.",
        "category": "페르소나",
        "favorite": False
    },
    {
        "title": "다이어트 고민 답변 생성",
        "content": "내가 지금 2달 동안 다이어트해서 4키로를 뺐는데, 최근 일주일 동안 스트레스를 엄청 받고 먹을 것으로 스트레스를 풀고 잠도 잘 못 잤어. 게다가 생리 1주일 전이라 그런지 4키로 뺐던 게 다시 다 쪄서 딱 2달 전 상태야. 지금 2달 동안 노력한 게 완전히 무너진 것 같아서 너무 막막해. 나에게 따뜻한 위로의 말을 해주고, 내일부터 다시 전처럼 다이어트를 잘할 수 있게 현실적인 행동 대안 3가지만 알려줘.",
        "category": "텍스트 생성",
        "favorite": False
    },
    {
        "title": "Dream X 광고 씬1 생성",
        "content": "자기 방에서 혼자 작게 흥얼거리는 모습. 수줍고 조심스러운 분위기. 처음에는 흥얼거리다가 한숨을 쉬고, 반드시 한국어로 '노래, 잘하고 싶은데...'라고 말한다. 영상 내부 자막은 생성하지 않는다. 마지막에는 아쉬운 표정을 짓는다. 세로형 영상.",
        "category": "영상 생성",
        "favorite": False
    },
    {
        "title": "Dream X 한강 버스킹 씬2 생성",
        "content": "맑은 낮의 한강공원에서 젊은 여성이 마이크를 들고 즐겁게 노래한다. 기타 연주자와 여러 관객이 박수를 치며 함께 즐긴다. 설레고 에너지 넘치는 분위기, 자연스러운 카메라 이동, 밝고 청량한 색감, 세로형 광고 영상. 영상 안에는 글자를 생성하지 않는다.",
        "category": "영상 생성",
        "favorite": False
    }
]


def show_menu():
    """사용할 수 있는 메뉴를 화면에 보여준다."""
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


def read_required(label):
    """빈 내용을 입력하면 다시 물어본다."""
    while True:
        value = input(label).strip()
        if value:
            return value
        print("빈 내용은 입력할 수 없습니다. 다시 입력해주세요.")


def choose_category():
    """정해진 카테고리 중 하나를 선택한다."""
    print("\n카테고리 선택:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}) {category}")
    while True:
        choice = input("카테고리 번호: ").strip()
        if choice in [str(number) for number in range(1, len(CATEGORIES) + 1)]:
            return CATEGORIES[int(choice) - 1]
        print("잘못된 카테고리 번호입니다. 1~6 중에서 선택해주세요.")


def add_prompt():
    """제목, 내용, 카테고리를 받아 새 프롬프트를 추가한다."""
    print("\n=== 프롬프트 추가 ===")
    title = read_required("제목: ")
    content = read_required("내용: ")
    category = choose_category()
    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False
    })
    print(f"'{title}' 프롬프트가 추가되었습니다!")


def main():
    """기능을 사용한 뒤 다시 메뉴로 돌아오는 실행 흐름."""
    try:
        while True:
            show_menu()
            choice = input("선택: ").strip()
            if choice == "0":
                print("프로그램을 종료합니다. 추가한 내용은 종료 시 초기화됩니다.")
                break
            elif choice == "1":
                add_prompt()
            elif choice in ["1", "2", "3", "4", "5", "6", "7"]:
                print("아직 준비 중인 기능입니다.")
            else:
                print("잘못된 메뉴 번호입니다. 0~7 중에서 선택해주세요.")
    except (EOFError, KeyboardInterrupt):
        print("\n입력이 끝나 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
