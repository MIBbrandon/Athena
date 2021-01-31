def checkSwapStepsMakesSense(desiredInteraction, swapSteps):
    for step in swapSteps:
        if step != "#" and step != "Done already" and not (
                step[0] == desiredInteraction[0] or step[0] == desiredInteraction[1]):
            print("Step: " + str(step))
            print("Desired Interaction: " + str(desiredInteraction))
            raise Exception("Something is fishy here")


def checkDesiredInteractionIsAchieved(desiredInteraction, newG_interactions):
    if not newG_interactions.has_edge(*desiredInteraction):
        raise Exception("DESIRED INTERACTION %s IS INCOMPLETE" % str(desiredInteraction))
    # else:
    #     print("DESIRED INTERACTION %s COMPLETED" % str(desiredInteraction))
