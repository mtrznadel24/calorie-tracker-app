import pytest

from app.core.exceptions import NotFoundError


@pytest.mark.integration
class TestFridgeProductRepository:
    async def test_get_fridge_product_list_no_products(
        self, fridge_product_repo, fridge
    ):
        result = await fridge_product_repo.get_fridge_product_list(
            fridge.id, False, None, 0, 10
        )
        assert result == []

    async def test_get_fridge_product_list_one_product(
        self, fridge_product_repo, fridge, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="banana",
            category=None,
            is_favourite=False,
            calories_100g=89,
            proteins_100g=1.1,
            fats_100g=0.3,
            carbs_100g=23,
        )

        result = await fridge_product_repo.get_fridge_product_list(
            fridge.id, False, None, 0, 10
        )

        assert result != []
        assert result[0] == product

    async def test_get_fridge_product_list_many_products(
        self, fridge_product_repo, fridge, fridge_product_factory
    ):
        products = [
            await fridge_product_factory(
                product_name=name,
                category=None,
                is_favourite=False,
                calories_100g=89,
                proteins_100g=1.1,
                fats_100g=0.3,
                carbs_100g=23,
            )
            for name in ["product1", "product2", "product3"]
        ]

        result = await fridge_product_repo.get_fridge_product_list(
            fridge.id, False, None, 0, 10
        )
        assert result == products

    async def test_get_fridge_product_list_favourite_products(
        self, fridge_product_repo, fridge, fridge_product_factory
    ):
        products = [
            await fridge_product_factory(
                product_name=name,
                category=None,
                is_favourite=is_favourite,
                calories_100g=89,
                proteins_100g=1.1,
                fats_100g=0.3,
                carbs_100g=23,
            )
            for name, is_favourite in [
                ("product1", True),
                ("product2", False),
                ("product3", True),
                ("product4", False),
            ]
        ]

        result = await fridge_product_repo.get_fridge_product_list(
            fridge.id, True, None, 0, 10
        )

        assert len(result) == 2
        assert result[0] == products[0]
        assert result[1] == products[2]

    async def test_get_fridge_product_list_skip_limit(
        self, fridge_product_repo, fridge, fridge_product_factory
    ):
        products = [
            await fridge_product_factory(
                product_name=name,
                category=None,
                is_favourite=False,
                calories_100g=89,
                proteins_100g=1.1,
                fats_100g=0.3,
                carbs_100g=23,
            )
            for name in ["product1", "product2", "product3", "product4"]
        ]

        result = await fridge_product_repo.get_fridge_product_list(
            fridge.id, False, None, 2, 4
        )

        assert len(result) == 2
        assert result[0] == products[2]
        assert result[1] == products[3]

    async def test_get_fridge_product(
        self, fridge_product_repo, fridge, sample_fridge_product
    ):
        result = await fridge_product_repo.get_fridge_product(
            fridge.id, sample_fridge_product.id
        )
        assert result == sample_fridge_product

    async def test_get_fridge_product_wrong_fridge_id(
        self, fridge_product_repo, fridge, sample_fridge_product
    ):
        with pytest.raises(NotFoundError):
            await fridge_product_repo.get_fridge_product(999, sample_fridge_product.id)

    async def test_get_fridge_product_wrong_product_id(
        self, fridge_product_repo, fridge, sample_fridge_product
    ):
        with pytest.raises(NotFoundError):
            await fridge_product_repo.get_fridge_product(fridge.id, 999)

    async def test_delete_fridge_product_wrong_product_id(
        self, fridge_product_repo, fridge
    ):
        with pytest.raises(NotFoundError):
            await fridge_product_repo.delete_fridge_product(fridge.id, 999)

    async def test_delete_fridge_product_success(
        self, fridge_product_repo, fridge, sample_fridge_product
    ):
        await fridge_product_repo.delete_fridge_product(
            fridge.id, sample_fridge_product.id
        )

        with pytest.raises(NotFoundError):
            await fridge_product_repo.get_fridge_product(
                fridge.id, sample_fridge_product.id
            )
