def transform_post_data(request):
    """Transform POST repeater data to formset data"""
    # TODO: Potentially insecure, add some key checking with RegExp
    transformed_post_keys = {}
    post_keys_to_delete = []
    for post_key, post_value in request.POST.items():
        if not post_key.startswith("kt_participants_repeater"):
            continue
        post_keys_to_delete.append(post_key)
        key_index = post_key.split("][")[0].split("[")[1]
        field_name = post_key.split("-")[-1].strip("]")
        new_post_key = f"form-{key_index}-{field_name}"
        transformed_post_keys[new_post_key] = post_value

    # Yes I know this is kinda hacky but it works
    request.POST._mutable = True  # pylint: disable=protected-access

    # Delete post keys
    for key_to_delete in post_keys_to_delete:
        del request.POST[key_to_delete]

    # Add new keys
    for key, item in transformed_post_keys.items():
        request.POST[key] = item

    # Yes I know this is kinda hacky but it works
    request.POST._mutable = False  # pylint: disable=protected-access

    return request
