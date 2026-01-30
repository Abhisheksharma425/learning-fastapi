from fastapi import APIRouter

router = APIRouter()

@router.get('/items/',tags = ['items'])
def read_items():
    return [{'item_id':'Foo'},{'item_id':'Bar'}]
