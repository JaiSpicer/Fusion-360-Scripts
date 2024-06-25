import adsk.core, adsk.fusion, adsk.cam, traceback, os

exportPath = "C:/Testing"

# Function to set appearances
def set_appearances(rootComp, ui):
    app = adsk.core.Application.get()
    try:
        # Access the specified library from the Application object, not the UserInterface
        customLib = app.materialLibraries.itemByName("FusionPrintingMaterials")
        blackPETG = customLib.appearances.itemByName("PETG (Black)")
        redPETG = customLib.appearances.itemByName("PETG (Red)")
    except Exception as e:
        ui.messageBox(f"Error accessing appearances: {str(e)}")
        return False

    for body in rootComp.bRepBodies:
        if body.name == "Base":
            body.appearance = blackPETG
        else:
            body.appearance = redPETG
    return True

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        # Ask the user for a comma-separated list of labels
        inputResult = ui.inputBox('Enter a comma-separated list of labels:', 'Labels Input')
        if inputResult[0]:
            labels = inputResult[0].split(',')

        for label in labels:
            label = label.strip()  # Remove leading/trailing whitespace
            if not label:
                continue  # Skip empty labels

            # Get the sketch named "Text"
            sk = rootComp.sketches.itemByName('Text')
            skText = sk.sketchTexts.item(0)
            skText.text = label  # Change the text

            # Set appearances before exporting
            if not set_appearances(rootComp, ui):
                return  # Exit if appearances could not be set

            # Get the current document's name
            document_name = design.rootComponent.name

            # Use the document name in the filename, ensuring it's a valid filename
            safe_document_name = ''.join([c for c in document_name if c.isalnum() or c in (' ', '_', '-')]).rstrip()
            # Specify the export filename and path
            safe_label = ''.join([c for c in label if c.isalnum() or c in (' ', '_', '-')]).rstrip()
            filename = rf"{exportPath}\{safe_document_name} - {safe_label}.3mf"

            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # Create the 3MF export options
            options = design.exportManager.createC3MFExportOptions(rootComp, filename)

            # Execute the export
            design.exportManager.execute(options)

    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:\n{e}')
