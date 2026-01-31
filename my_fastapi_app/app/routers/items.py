from fastapi import APIRouter,Depends
from app.dependencies import common_pagination

router = APIRouter()

@router.get('/',tags = ['items'])
def read_items(commons:dict = Depends(common_pagination)):
    return [{'messages':[{'item_id':'Foo'},{'item_id':'Bar'}],
             'commons':commons}]

@router.get('/{items_id}',tags = ['items'])
def read_items(items_id:str):
    return {'items_id':items_id}