<?php
use Tests\TestCase;
use Illuminate\Foundation\Testing\WithFaker;
use Illuminate\Foundation\Testing\RefreshDatabase;

class CreatePostsTest extends TestCase
{
    use withFaker, RefreshDatabase; 
    
    // @test
    function test_a_user_can_create_a_post()
    {
        $this->withoutExceptionHandling();
        
        // Having
        $attributes = [
            'title' => $this->faker->sentence,
            'content' => $this->faker->paragraph,
        ];

        $this->post('/posts', $attributes)->assertRedirect('/posts');

        // Then
        $this->assertDatabaseHas('posts', $attributes);

        $this->get('/posts')->assertSee($attributes['title']);

    }
}
