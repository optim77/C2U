import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Landpage from "./pages/Landpage";
import CategoryPage from "./pages/CategoryPage";

function Main() {
    return (
        <Routes>
            <Route path="/" element={<Landpage />} />
            <Route path="/category/:id" element={<CategoryPage />} />
        </Routes>
    );
}

export default Main;
