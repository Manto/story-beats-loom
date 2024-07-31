import story_beats_loom

def test_placeholder():
    story = story_beats_loom.StoryBeatsLoom(None)
    
    assert story is not None