from mcp.server.fastmcp import FastMCP

from tools.resume import parse_resume

from tools.profile import generate_resume_description

from tools.search import search_jobs

mcp = FastMCP("job-ai-agent")

# Register tools

mcp.tool()(parse_resume)
mcp.tool()(generate_resume_description)
mcp.tool()(search_jobs)
mcp.verbose = True

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")




# from mcp.server.fastmcp import FastMCP

# # Create an MCP server
# mcp = FastMCP("Demo", json_response=True)


# # Add an addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b


# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"


# # Add a prompt
# @mcp.prompt()
# def greet_user(name: str, style: str = "friendly") -> str:
#     """Generate a greeting prompt"""
#     styles = {
#         "friendly": "Please write a warm, friendly greeting",
#         "formal": "Please write a formal, professional greeting",
#         "casual": "Please write a casual, relaxed greeting",
#     }

#     return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run()
