from notion.client import NotionClient
from notion.block import TodoBlock
from notion.block import PageBlock
from notion.block import TextBlock
from notion.block import CollectionViewBlock
from notion.block import VideoBlock
from notion.block import HeaderBlock
import configparser
import json


def get_collection_schema():
    return {
        "%9:q": {"name": "Check Yo'self", "type": "checkbox"},
        "=d{|": {
            "name": "Tags",
            "type": "multi_select",
            "options": [
                {
                    "color": "orange",
                    "id": "79560dab-c776-43d1-9420-27f4011fcaec",
                    "value": "A",
                },
                {
                    "color": "default",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c44",
                    "value": "B",
                },
                {
                    "color": "blue",
                    "id": "77f431ab-aeb2-48c2-9e40-3a630fb86a5b",
                    "value": "C",
                },
            ],
        },
        "=d{q": {
            "name": "Category",
            "type": "select",
            "options": [
                {
                    "color": "orange",
                    "id": "59560dab-c776-43d1-9420-27f4011fcaec",
                    "value": "A",
                },
                {
                    "color": "default",
                    "id": "502c7016-ac57-413a-90a6-64afadfb0c44",
                    "value": "B",
                },
                {
                    "color": "blue",
                    "id": "57f431ab-aeb2-48c2-9e40-3a630fb86a5b",
                    "value": "C",
                },
            ],
        },
        "LL[(": {"name": "Person", "type": "person"},
        "title": {"name": "Name", "type": "title"},
    }


def operation_to_notion():
    # configuration
    with open('config.json', 'r') as f:
        config = json.load(f)

    # login
    token_v2 = config['token']
    client = NotionClient(token_v2=token_v2)

    # page url
    url = config['pageUrl']
    page = client.get_block(url)

    print("Page 제목은 : ", page.title)

    # API 호출로 Page Block 추가
    print(page.children.add_new(PageBlock, title="페이지 만들기"))

    # API 호출로 Text Block 추가
    print(page.children.add_new(TextBlock, title="텍스트 쓰기"))

    # API 호출로 비디오 블록 삽입
    page.children.add_new(HeaderBlock, title="cigarettes after sex￼ - sweet")
    video = page.children.add_new(VideoBlock, width=200)
    video.set_source_url("https://www.youtube.com/watch?v=QjYRRNNwZiM&t=167s")

    # API 호출로 Inline Table 추가
    collection_view_block = page.children.add_new(CollectionViewBlock)
    collection_view_block.collection = client.get_collection(
        client.create_record(
            "collection", parent=collection_view_block, schema=get_collection_schema())
    )
    collection_view_block.title = "내 데이터"
    view = collection_view_block.views.add_new(view_type="table")
    row = collection_view_block.collection.add_row()
    assert row.person == []
    row.name = "JohnMark"
    row.title = "Notion Unofficial API Tets"
    assert row.name == row.title
    row.check_yo_self = True
    row.person = client.current_user
    row.tags = ["A", "C"]
    row.category = "A"
    print(view.default_query().execute())
    return "Done."

if __name__ == "__main__":
    result = operation_to_notion()
    print(result)