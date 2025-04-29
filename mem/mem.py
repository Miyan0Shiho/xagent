"""
这里主动给mcp提供一个工具,让其可以利用rag从数据库中查询长期记忆
传入json格式数据如下：
{
    '会话id':'',
    '用户id':''
    '会话':{
        {
            'system':'',
            'user':'',
            'time':'',

        }
    }
    '会话时间':,
    '精炼后记忆':
}

接口定义如下: writelongtermem(connversation,agentid)
            readflongrtermem(agentid,starttime, endtime)
"""


