
from typing import Any
from realtime_agent.tools import ToolContext

# Function calling Example
# This is an example of how to add a new function to the agent tools.

class AgentTools(ToolContext):
    def __init__(self) -> None:
        super().__init__()
        
        # create multiple functions here as per requirement
        self.register_function(
            name="get_avg_temp",
            description="Returns average temperature of a country",
            parameters={
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Name of country",
                    },
                },
                "required": ["country"],
            },
            fn=self._get_avg_temperature_by_country_name,
        )

    async def _get_avg_temperature_by_country_name(
        self,
        country: str,
    ) -> dict[str, Any]:
        try:
            result = "24 degree C" # Dummy data (Get the Required value here, like a DB call or API call)
            return {
                "status": "success",
                "message": f"Average temperature of {country} is {result}",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get : {str(e)}",
            }