from model.prediction_brows import predict_brows
from model.prediction_face_shape import predict_shape
from model.eye_distance import check_eye_spacing
import cv2

def get_face_features(picture_path):
    
    eye_spacing = check_eye_spacing(picture_path)
    face_shape = predict_shape(picture_path)
    brows_shape = predict_brows(picture_path)
    
    
    return eye_spacing, face_shape, brows_shape


def compute_P(selected_colors: list, selected_brands: list,
              stars_color, stars_brand,
              frames_color, frames_brand):


    stars_sum = stars_color + stars_brand
    star_value = 0.3 / stars_sum

    P = 0


    if frames_color in selected_colors:
        P += stars_color * star_value


    if frames_brand in selected_brands:
        P += stars_brand * star_value

    return P


def compute_score_per_frame(
    s_ai_impact_val, ai_shapes, ai_types,
    types_selected, shapes_selected,
    frames_shape, frames_type, P):

    S = 0
    U = 0
    u_user_impact_val = 1 - s_ai_impact_val

    # Dopasowanie oparte na AI
    if frames_shape in ai_shapes:
        S += 0.4 * ai_shapes[frames_shape]  # maks. 0.6
    for t_type, weight in ai_types:
        if frames_type == t_type:
            S += 0.4 * (weight / 5)          # maks. 0.4
    S = min(S, 1.0)

    U = 0

    # Sprawdzenie materiału oprawki
    if frames_type in types_selected:
        U += 0.4

    # Sprawdzenie kształtu oprawki
    if frames_shape in shapes_selected:
        U += 0.4

    # Maksymalnie 0.8
    U = min(U, 0.8)

    P = min(P, 0.3)

    # Końcowy wynik (maks. 1.0)
    base_score = (u_user_impact_val * U + s_ai_impact_val * S)
    R = 0.7 * base_score + P

    return R


def main(user_data, frames):


    recommendations = []

    for frame in frames:
        frame_color = frame.get("color", "")
        frame_brand = frame.get("mark", "")
        frame_shape = frame.get("shape", "")
        frame_type = frame.get("type", "")

        # compute P (no price)
        P = compute_P(
            selected_colors=user_data["colors"],
            selected_brands=user_data["marks"],
            stars_color=user_data["stars_color"],
            stars_brand=user_data["stars_brand"],
            frames_color=frame_color,
            frames_brand=frame_brand
        )

        # compute score
        score = compute_score_per_frame(
            s_ai_impact_val=user_data["ai_impact"],
            ai_shapes=user_data["ai_shape"],
            ai_types=user_data["ai_type"],
            types_selected=user_data["type"],
            shapes_selected=user_data["shape"],
            frames_shape=frame_shape,
            frames_type=frame_type,
            P=P
        )

        recommendations.append({
            **frame,
            "score": score
        })

    # sort by score descending
    recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)
    return recommendations
