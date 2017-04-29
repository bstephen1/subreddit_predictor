
goals for the scraper:
  -get data (defined below) from a number of subreddits
    -should be easy to modify which subreddits it gets data from
    -possibly only work with the defaults, or a subset of them
  -data formated as a vector:
    -post title 
    -type of post (text, link, etc)
    -post content (if a text post, this should be the text, but if the post is a link it should be the link.
      Note that these fields are probably located in different places.)
      -Possibly account for a text post where the text is just a link. (These may not be that frequent, could ignore)
      -if a link, just parse the domain name.
    -comments
      -Should just be the text of the comment. Don't need username, upvotes, etc. 
      -Should be easy to change how many comments it pulls. 5 or so is probably a good starting point.
      -Also need to determine which comments are pulled. It defaults to "best" sorting, so that may be the way to go.
      -Pull only top-level comments, or child comments as well? It wouldn't be too hard to add child comments, 
        but it would be harder to do something like "top 5 comments".
      -what about comment karma? Should it ignore comments below a certain threshold? They may not be indicitive of the
        sub's content.
      -what if a comment has a link? Parse the domain name as with the post content?
      -deleted comments: should just skip these 
     -other:
      -probably best to sort by top of all time. Will be the most upvoted content so most likely to be the "essence" 
        of the sub. Will also give a large amount of comments to work with. Won't have to deal with not enough comments.
      -easiest way to do comments would be to get the first X top-level comments. That probably works well enough to get
        the gist of how people react to the post. Would also minimize "meme chains", as those are generally limited to a single
        comment chain. 
      -any other data needed? Upvotes, date posted, number of comments, usernames -- any of these useful?
        -possibly if the comment was gilded. Seems like a pain to implement for not much reward. 
        -user flair could be pretty helpful. Some subs have themed flair so that would be a dead giveaway.
          -this is located in a "flair" class within the "tagline" class, as a title field. Shouldn't be 
            too hard to pull.
          -flair is also per-sub, so the same user can have a different flair on each sub
      -Note: it seems that if comments have a newline, it separates the comment into multiple paragraphs. The entire comment
        is in an "md" class, so all of its contents have to be pulled.
      -promoted posts: skip these. might be easiest to skip the first post. From a cursory glance, it looks like these posts
         are structured very similar to normal posts
