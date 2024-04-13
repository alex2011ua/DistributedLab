#!/usr/bin/env python3
import asyncio
import time

from aiohttp import ClientError, ClientSession


class Node:
    visited: set = set()
    counter: int = 0

    def __init__(self, children, name=None, parent=None, depth=0):
        self.name: str | None = name
        self.children: list = children
        self.parent: Node | None = parent
        self.depth: int = depth
        Node.counter += 1

    def __str__(self):
        return f"Node: {self.name}, depth: {self.depth}, children: {len(self.children)}"

    def __repr__(self):
        return self.name

    def print_path_to_root(self) -> None:
        """Print a path from current node to root node."""

        if self.name:
            print("https://en.wikipedia.org/wiki/" + self.name.replace(' ', '_'))
        if self.parent is not None:
            return self.parent.print_path_to_root()


async def fetch_page_links(page_children, session, node_parent) -> Node | None:
    """Request to wikipedia API and parse the response to make a node"""

    # https://www.mediawiki.org/wiki/API:Main_page
    api_url = "https://en.wikipedia.org/w/api.php"  # Wikipedia API endpoint
    params = {
        "action": "query",
        "format": "json",
        "titles": page_children,
        "prop": "links",
        "pllimit": "max"
    }
    try:
        async with session.get(api_url, params=params) as response:
            if response.status == 429:
                """We recommend making a reasonable number of calls to prevent getting blocked. 
                If you want to make many requests, contact the administrators beforehand."""
                time.sleep(1)
                return await fetch_page_links(page_children, session, node_parent)

            titles = []
            data = await response.json()
            # Scan article  for other Wikipedia links
            pages = data.get('query', {}).get('pages', {})
            for page_id in pages:
                page = pages[page_id]
                links = page.get('links', [])
                for link in links:
                    title = link.get('title')
                    if title not in Node.visited:  # add only those links that have not been visited
                        titles.append(title)
                        Node.visited.add(title)
            if titles:  # a page without links is not needed
                return Node(parent=node_parent, name=page_children, children=titles, depth=node_parent.depth + 1)
    except ClientError as e:
        print(f"Failed to fetch {page_children}: {e}")
        return None

async def fetch_child_nodes(node_parent: Node) -> list[Node]:
    """Creating a list of nodes from a parent node"""

    async with ClientSession() as session:
        tasks = []
        for page_children in node_parent.children:
            tasks.append(asyncio.create_task(fetch_page_links(page_children, session, node_parent)))
        results = await asyncio.gather(*tasks)
    children = [node for node in results if node is not None]
    return children


async def main(start_page, finish_page) -> None:
    """
    Receives a Wikipedia article and scans it for other Wikipedia links,
    opens them, and scans for links until it finds the link
    """

    root_node: Node = Node(children=[start_page])  # Create root node with start page in children list
    nodes: list[Node] = [root_node]  # list of nodes to search next level nodes

    for depth in range(7):
        print(f"Depth {depth}: Searching...")
        for node in nodes:
            if finish_page in node.children:  # article with Hitler found
                print("Hitler found")
                print("https://en.wikipedia.org/wiki/" + finish_page.replace(' ', '_'))
                node.print_path_to_root()  # Print path to article
                print(f"visited {Node.counter} pages.")
                return
        new_nodes = await asyncio.gather(*[fetch_child_nodes(node) for node in nodes])
        nodes.clear()
        nodes.extend(*new_nodes)
    print("Hitler not found")

if __name__ == '__main__':
    input_link = input("Enter a link: ")
    start_page = input_link[input_link.rfind("/") + 1:].replace("_", " ")
    finish_page = "Adolf Hitler"
    asyncio.run(main(start_page, finish_page))
