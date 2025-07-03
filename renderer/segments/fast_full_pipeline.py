from segments.intro import generate_intro_segment
from segments.question import generate_question_segment
from segments.answers import generate_answers_segment
from segments.countdown import generate_countdown_segment
from segments.reveal import generate_reveal_segment
from segments.final_video import generate_fast_final_video

def fast_full_pipeline(slug: str):
    """
    Automatycznie generuje wszystkie segmenty i finalne wideo.
    """
    print("Starting full pipeline...")
    generate_intro_segment(slug)
    generate_question_segment(slug)
    generate_answers_segment(slug)
    generate_countdown_segment(slug)
    generate_reveal_segment(slug)
    final_video = generate_fast_final_video(slug)
    print(f"Full pipeline completed: {final_video}")
    return final_video
