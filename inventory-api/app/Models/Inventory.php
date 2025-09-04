<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Inventory extends Model
{
   use HasFactory;
   protected $fillable = ['name','quantity','price'];
}
