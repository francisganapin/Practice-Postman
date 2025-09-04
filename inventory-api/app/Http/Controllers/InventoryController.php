<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Inventory;

class InventoryController extends Controller
{
    public function index()
    {
        return Inventory::all();
    }

    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required|string',
            'quantity' => 'required|integer|min:0',
            'price' => 'required|numeric|min:0',
        ]);

        return Inventory::create($request->all());
    }

    public function show(string $id)
    {
        return Inventory::findOrFail($id);
    }

    public function update(Request $request, string $id)
    {
        $inventory = Inventory::findOrFail($id);
        $inventory->update($request->all());

        return $inventory;
    }

    public function destroy(string $id)
    {
        return Inventory::destroy($id);
    }
}
