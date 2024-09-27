import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

function CategoryPage() {
    const { id } = useParams(); // Pobieranie id z parametrów URL
    const [category, setCategory] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        const fetchCategory = async () => {
            const res = await fetch(`http://localhost:8000/api/tools/category/${id}`);
            const data = await res.json();
            setCategory(data);
            setIsLoaded(true);
        };

        fetchCategory();
    }, [id]);

    return (
        <div>
            {isLoaded ? (
                <div>
                    <h1>{category.name}</h1>
                    <p>{category.description}</p>
                    <img src={category.image} alt={category.name} />
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default CategoryPage;
