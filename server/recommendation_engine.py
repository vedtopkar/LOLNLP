def gif_within_distance(x0, y0, xs, ys, r, a):
    """
    Given an (x,y) coordinate and a distance
    Return all GIFs within that radius
    """
    
    bools = []
    
    for i in range(len(xs)):
        bools.append(r >= hypot(a*x0-xs[i], a*y0-ys[i]))
        
    return bools

def gifs_in_neighborhood(x, y, df, xidx='GIF_x', yidx='GIF_y', r=0.05, a=1.0):
    """
    Iteratively expand the radius of searching
    Until we get a hit for the closest GIF in the area
    """
    
    xs = df[xidx]
    ys = df[yidx]
    bool_mask = gif_within_distance(x, y, xs, ys, r, a)
    while sum(bool_mask) == 0:
        r += 0.05
        bool_mask = gif_within_distance(x, y, xs, ys, r, a)

    return df[bool_mask]

def recommend_GIFs(text, amplify=1.0, verbose = False):
    """
    Given a piece of text, search for the best GIF
    Combines the content and sentiment NLP analysis implemented above
    """
    sentiment = estimate_phrase_sentiment(text)
    if not sentiment:
       gifs = find_matching_gifs_by_content(text, output=False)
    else:
        gifs = gifs_in_neighborhood(sentiment[0], sentiment[1], master, r=0.8, a=amplify)
    
        content_gifs = find_matching_gifs_by_content(text, output=False)
        specific_gifs = gifs.merge(content_gifs, on='URL')
    
        if len(specific_gifs)>0:
            gifs = specific_gifs

    return gifs

def recommend_gif(text):
    """
    Given a piece of text, get all of the relevant gifs
    Then return a random gif from the results (of the subset that is closest to the results)
    """
    
    gifs = recommend_GIFs(text)

    max_content_matches = max(gifs['N Matches'])
    gif = gifs[gifs['N Matches'] == max_content_matches].iloc[random.randint(0, len(gifs)-1)]
    gif_url = gif['URL']

    return gif_url