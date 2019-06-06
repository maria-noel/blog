<?php

namespace Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithFaker;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Faker\Factory;
use App\User;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class UserTest extends TestCase
{
    use DatabaseTransactions;
    /**
     * A basic feature test example.
     *
     * @return void
     */
    public function testExample()
    {
        $name = 'Maria';
        $email = 'maria@dev.com';
        
        $user = factory(User::class)->create([
            'name' => $name,
            'email' => $email,
        ]);

        $response = $this->actingAs($user, 'api')
        ->get('/api/user')
        ->assertSee($name)
        ->assertSee($email);

        // $response->assertStatus(200);
    }
}
