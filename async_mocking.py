import asyncio
from unittest.mock import AsyncMock, patch
import pytest

async def run_cmd(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    print(proc.returncode)
    print(stdout)


async def main():

    cmds = ["sleep 5; echo Hello, World", "sleep 5; echo Hello, Python"]

    coroutines  = [run_cmd(c) for c in cmds]
    res = await asyncio.gather(*coroutines)
    return res

if __name__ == "__main__":

    asyncio.run(main())

@pytest.mark.asyncio
async def test_main():
    
    with patch('asyncio.create_subprocess_shell') as mock_create_subprocess:
        mock_proc = AsyncMock()
        mock_proc.communicate.side_effect = [(b"Mock stdout", b"Mock stderr"),(b"Mock stdout 2", b"Mock stderr 2")]
        mock_proc.returncode = 0
        mock_create_subprocess.return_value = mock_proc

        res = await main()

        assert mock_create_subprocess.await_count == 2
