import useCartStore from '../../store/cartStore';

export const useCart = ()=>{
    const { items, totalItems, totalPrice, addItem, removeItem, clearCart} = useCartStore();
    return { items, totalItems, totalPrice, addItem, removeItem, clearCart};
};