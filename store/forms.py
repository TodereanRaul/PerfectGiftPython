from django import forms

from store.models import Order

class OrderForm(forms.ModelForm):
    quantity = forms.ChoiceField(choices=[(i, i) for i in range(1, 11)]) 
    # allow user to delete one item from the cart
    delete = forms.BooleanField(required=False, label="Supprimer l'article", initial=False)

    # Meta class is used to specify the model and fields
    class Meta:
        model = Order
        fields = ['quantity']

    def save(self, *args, **kwargs):
        # get data from the form using a dictionary 
        # if delete is checked, delete the instance
        if self.cleaned_data["delete"]:
            self.instance.delete()
            # if no items in the cart, delete the cart
            if self.instance.user.cart.orders.count() == 0:
                self.instance.user.cart.delete()
            return True
        return super().save(*args, **kwargs)