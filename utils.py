def get_color(party, vote_percentage, max_value, min_value=0.2):
    party_colors = {
        'Democrat': (0, 0, 255),  # Blue
        'Republican': (255, 0, 0)   # Red
    }
    
    r_party, g_party, b_party = party_colors.get(party, (0, 255, 0))  # Default to Green for other parties
    
    normalized_percentage = (vote_percentage - min_value) / ( max_value - min_value)

    # Calculate the color based on the normalized vote percentagee
    r = int(255 * (1 - normalized_percentage) + r_party * (normalized_percentage))
    g = int(255 * (1 - normalized_percentage) + g_party * (normalized_percentage))
    b = int(255 * (1 - normalized_percentage) + b_party * (normalized_percentage))
    
    color = f"rgb({r}, {g}, {b})"
    return color