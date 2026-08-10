Issue1 : whole Blog was going as input to decide_image place and coming out as output which is hevy process  ?
Solutiion : We passed anchor_Text as State and took that only where to keep image 


Issue2 : "Blog generation failed for thread_id=f86cf92b-4447-460b-898e-b47154f3b195: ValueError: decide_images: anchor text not found for [[IMAGE_1]]: "Creating clear and flexible route handlers in FastAPI involves defining endpoints that can accept both path and query parameters. Here's an example:" : Directly Getting Passed to use and not getting option of try again 
Solution : 
    1. Need to use Sync postgressSAver for Checkpoint which help's fault tolerance and user can restart process again or we will do automation here with 3 tries 
    2. why sync because celery worker pool runs each task as a regular synchronous python function in seperate process. There is no event loop running unless you build one. 
    3. I may prefer AsynPostgressSaver when graph itself does concurrent asyncIo which helps multiple parallel LLM calls,Parallel Image Generation also we are invoking graph with invoke not ainvoke 
    4.

Issue: decide_images: anchor text not found for [[IMAGE_2]]: 'This code snippet demonstrates a simple example of a smart contract written in Solidity.'  Failing and Crashing whole generation 
Solution : Fuzzy match (difflib, threshold=0.75) first, then silently skip image if still not found. No crash.

Issue: Storage_logic seems little bit hard 















