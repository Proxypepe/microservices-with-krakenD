import logging
import httpx
import json

from rocketry import Rocketry
from rocketry.conds import every

import errors

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Rocketry(config={"task_execution": "async"})
url = 'http://product_service:8000'


@app.task(every("10 seconds"))
@errors.HTTP_handler(logger)
async def check_product_service_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{url}/_health")
        response.raise_for_status()
        assert json.loads(response.content.decode()) == {'status': 'Ok'}, errors.HTTPContent(f'Incorrect content')


if __name__ == "__main__":
    app.run()
