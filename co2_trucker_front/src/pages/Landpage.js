import {useEffect, useState} from "react";
import {Link} from "react-router-dom";

function Landpage() {

    const [categories, setCategories] = useState([]);
    const [isLoaded, setIsLoaded] = useState(false)
    useEffect(() => {
        const fetchCategories = async () => {
            await fetch('http://localhost:8000/api/categories', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            }).then((res) => {
                if (res.ok) {
                    res.json().then(data => {
                        setCategories(data.results);
                        setIsLoaded(true)
                        console.log(data.results)
                    })
                }
            })
        }
        fetchCategories();
    }, []);


    return (
        <>
            {isLoaded ? (
                <div className="container text-white">
                    <h1 className="text-center mt-5 display-4">CO2UNTER</h1>
                    <div className="container">
                        <div className="row">
                            {categories.map((category) => (
                                <div key={category.id} className="col-4 text-center">
                                    <Link to={`/category/${category.id}`}> {/* Link do widoku kategorii */}
                                        <img className="rounded" width="50%" src={category.image} alt={category.name} />
                                    </Link>
                                    <Link to={`/category/${category.id}`}>
                                        <p>{category.name}</p> {/* Link do nazwy kategorii */}
                                    </Link>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </>
    );

}

export default Landpage