from typing import Dict, Any, Union, List, Sequence, Callable

from aiocqhttp import CQHttp, Error as CQHttpError

from . import expression


def context_source(ctx: Dict[str, Any]) -> str:
    src = ''
    if ctx.get('group_id'):
        src += f'/group/{ctx["group_id"]}'
    elif ctx.get('discuss_id'):
        src += f'/discuss/{ctx["discuss_id"]}'
    if ctx.get('user_id'):
        src += f'/user/{ctx["user_id"]}'
    return src


async def send(bot: CQHttp, ctx: Dict[str, Any],
               message: Union[str, Dict[str, Any], List[Dict[str, Any]]],
               *, ignore_failure: bool = True) -> None:
    try:
        if ctx.get('post_type') == 'message':
            await bot.send(ctx, message)
        else:
            ctx = ctx.copy()
            if 'message' in ctx:
                del ctx['message']
            if 'group_id' in ctx:
                await bot.send_group_msg(**ctx, message=message)
            elif 'discuss_id' in ctx:
                await bot.send_discuss_msg(**ctx, message=message)
            elif 'user_id' in ctx:
                await bot.send_private_msg(**ctx, message=message)
    except CQHttpError:
        if not ignore_failure:
            raise


async def send_expr(bot: CQHttp, ctx: Dict[str, Any],
                    expr: Union[str, Sequence[str], Callable],
                    **kwargs):
    return await send(bot, ctx, expression.render(expr, **kwargs))