from django import forms


class QuantityChangeForm(forms.Form):
    New_quantity = forms.IntegerField()
    Cart_contentID = forms.CharField(widget = forms.HiddenInput)

class ItemRemoveForm(forms.Form):
    Cart_contentID = forms.CharField(widget = forms.HiddenInput)

#Form for deleting an item in the Save for later table
class DeleteSFLForm(forms.Form):
    Saved_ContentID = forms.CharField(widget = forms.HiddenInput)

class MoveCartItemToSFLForm(forms.Form):
    Cart_contentID = forms.CharField(widget = forms.HiddenInput)
    #Saved_contentID = forms.CharField(widget = forms.HiddenInput)

class MoveSflToCartForm(forms.Form):
    Saved_contentID = forms.CharField(widget = forms.HiddenInput)

class AddItemForm(forms.Form):
    ISBN = forms.CharField(widget = forms.HiddenInput)


