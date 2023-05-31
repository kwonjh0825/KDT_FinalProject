# KDT_FinalProject


Comment html들

- planet_contract.html

{% comment %}  
    {% for termofservice in termsofservice %}
    <div class="my-4">
        <div class="flex gap-8">
            <div class="w-10 h-10 rounded-full bg-[#ffd951] flex justify-center items-center">
            <span class="text-white font-bold">{{ termofservice.order }}</span>
            </div>
            <p>{{ termofservice.content|linebreaksbr }}</p>
        </div>
      </div>
      <hr class="border-gray-500">
      {% endfor %} 
{% endcomment %}

{% comment %} 
<div>
    <p class="mb-7 text-4xl text-center">몇가지 주의사항이 있습니다</p>
  {% for termofservice in termsofservice %}
    <h3>{{ termofservice.order }} {{ termofservice.content|linebreaksbr }}</h3>
  {% endfor %}
  
  <h3>위 이용 약관에 동의하십니까?</h3>
  <input type="checkbox" id="terms-checkbox"> 이용 약관에 동의합니다.
</div> 
{% endcomment %}



- planet_join.html

{% comment %} 
<div>
  <form id="profile-form" action="{% url 'planets:planet_join' planet.name %}" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <img id="preview1">
    <button onclick="document.getElementById('profile_image').click();" class="ml-1 mt-2 block text-lg font-medium text-slate-300"><span class="material-symbols-outlined">
      person_add
      </span></button>
    <input onchange="readURL1(this);" type="file" id="profile_image" name="profile_image" value="{{ user.profile_image }}" class="form-input mt-1 rounded-md bg-[#101013]" style="display: none;">
    
    <img id="preview2">
    <button onclick="document.getElementById('background_image').click();" class="ml-1 mt-2 block text-lg font-medium text-slate-300"><span class="material-symbols-outlined">
      add_photo_alternate
      </span></button>
    <input onchange="readURL2(this);" type="file" id="background_image" name="background_image" value="{{ user.background_image }}" class="form-input mt-1 rounded-md bg-[#101013]" style="display: none;">
    
    <div class="grid my-4">
      <button id="create-profile-btn" class="btn bg-[#ffd951] text-white font-bold py-2 px-4 rounded" type="submit">행성 프로필 생성</button>
    </div>
  </form>
</div> 
{% endcomment %}